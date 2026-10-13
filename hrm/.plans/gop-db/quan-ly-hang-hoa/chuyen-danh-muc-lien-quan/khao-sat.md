# Khảo sát 11 màn danh mục ERP — Phase 1

> Bước 1 của skill `erp-to-hrm-screen`: chỉ lấy **nghiệp vụ**, chưa động code HRM.
> Khảo sát 20/09/2026 trên nhánh `gop_db`, DB gộp `hrm_erp`. Tất cả số liệu đo thật.

## 1. Bảng tổng hợp 11 màn

| # | Màn ERP | Route index | Controller | Bảng | Dòng |
|---|---|---|---|---|---|
| 1 | Danh mục model | `model.index` | `Sale\ProductModelsController` | `product_models` | 39.796 |
| 2 | Danh mục code đặt hàng | `barcode.index` | `Sale\BarcodesController` | `barcodes` | 8.664 |
| 3 | Danh mục đơn vị tính | `unitIndex` | `Sale\UnitsController` | `units` | 145 |
| 4 | Danh mục thuộc tính | `attributeIndex` | `Sale\AttributesController` | `attributes` | 446 |
| 5 | Danh mục đơn vị thuộc tính | `unitechesIndex` | `Sale\UnitechsController` | `unitteches` | 103 |
| 6 | Danh mục thương hiệu | `brandList` | `Sale\BrandsController` | `brands` | 1.250 |
| 7 | Danh mục hãng sản xuất | `manufacIndex` | `Sale\ManufacturesController` | `manufactures` | 1.071 |
| 8 | Danh mục xuất xứ | `originIndex` | `Sale\OriginsController` | `origins` | 113 |
| 9 | Danh mục file đính kèm | `AttachmentType.index` | `Common\AttachmentTypeController` | `attachment_types` | 8 |
| 10 | Danh mục mã màu | `codeColorIndex` | `Common\CodeColorController` | `code_colors` | **0** |
| 11 | Danh mục thuế suất | `taxRates.index` | `Common\TaxRatesController` | `tax_rates` | 40 |

## 2. Schema thật (SHOW COLUMNS, `!` = NOT NULL)

| Bảng | Cột |
|---|---|
| `product_models` | id · **name!** · created_by! · updated_by · status! · timestamps · old_name |
| `barcodes` | id · **name!** · **manufacture_id!** · created_by! · updated_by · status! · timestamps |
| `units` | id · status! · **name!** · code · position · created_by! · updated_by · timestamps · **english_name** · **can_be_base!** |
| `attributes` | id · status! · **name!** · attributeset_id · **is_filter!** · position · created_by! · updated_by · timestamps |
| `unitteches` | id · **name!** · note · position · created_by! · updated_by · timestamps · status! |
| `brands` | id · status! · **name!** · **code!** · icon · position · image · created_by! · updated_by · timestamps · **company_id** |
| `manufactures` | id · status! · **name!** · icon · position · image · created_by! · updated_by · timestamps · code · **buyer_id** · **deputy_id** · **has_vat!** · represent_id · **since_delivery_time** · **since_approved_time** · **since_PO_time** · **since_PI_time** · **company_id** |
| `origins` | id · status! · **name!** · icon · position · image · created_by! · updated_by · timestamps |
| `attachment_types` | id · **code!** · **name!** · description · status! · created_by! · updated_by! · **company_id!** · **department_id!** · part_id · timestamps |
| `code_colors` | id · **code!** · **name!** · note · status! · created_by! · updated_by! · **company_id!** · **department_id!** · timestamps |
| `tax_rates` | id · **tax_rate!** (decimal) · **is_sales_tax!** · **is_purchases_tax!** · status! · **created_by! (varchar)** · **updated_by! (varchar)** · timestamps |

Chỉ **4/11 bảng có cột `code`**: `units` (nullable) · `brands` · `attachment_types` · `code_colors`.
`manufactures.code` có nhưng nullable. 6 bảng còn lại **không có mã**.

## 3. Trạng thái — ERP dùng 0/1, KHÔNG phải 1/2 của HRM

Đếm thật theo `status`:

| Bảng | 0 (Khóa) | 1 (Hoạt động) |
|---|---|---|
| `product_models` | 268 | 39.528 |
| `barcodes` | 0 | 8.664 |
| `units` | 1 | 144 |
| `attributes` | 2 | 444 |
| `unitteches` | 0 | 103 |
| `brands` | 6 | 1.244 |
| `manufactures` | 59 | 1.012 |
| `origins` | 1 | 112 |
| `attachment_types` | 0 | 8 |
| `code_colors` | — | — (bảng rỗng) |
| `tax_rates` | 0 | 40 |

Blade ERP render: `data == 0` → `Khóa` (đỏ) · ngược lại → `Hoạt động` (xanh).
Chuẩn HRM là **1 = Hoạt động, 2 = Khóa** (Phase 0 dùng chuẩn này vì bảng mới, ERP không đọc).
⚠️ 11 bảng này **ERP vẫn đang đọc** → đổi số trong DB là đụng ERP đang chạy.

## 4. Mức độ bị tham chiếu — đây là master data lõi, không phải danh mục lẻ

Đếm số bảng trong DB gộp có cột khoá ngoại tương ứng:

| Cột | Trỏ tới | Số bảng có cột này |
|---|---|---|
| `unit_id` | `units` | **234** |
| `brand_id` | `brands` | **111** |
| `manufacture_id` | `manufactures` | **56** |
| `origin_id` | `origins` | **46** |
| `attribute_id` | `attributes` | 7 |
| `barcode_id` | `barcodes` | 7 |
| `attachment_type_id` | `attachment_types` | 5 |
| `unittech_id` | `unitteches` | 4 |
| `product_model_id` · `tax_rate_id` · `code_color_id` | — | 0 (nối bằng tên/cách khác) |

Số file ERP còn gọi model tương ứng (php / blade):
`Unit` 217/16 · `Brand` 82/139 · `Manufacture` 81/124 · `ProductModel` 62/29 · `Origin` 55/28 ·
`Barcode` 37/26 · `Attribute` 20/0 · `Unittech` 17/5 · `TaxRate` 14/4 · `CodeColor` 3/9 ·
`AttachmentType` 0/7.

→ **Không có chuyện "chuyển bảng sang HRM"**. DB đã gộp, cùng một bảng. Việc của Phase 1 là
**dựng màn quản lý bên HRM trên đúng bảng đó**.

## 5. Quyền ERP — DÙNG CHUNG với nhóm "Hàng hóa có sẵn" (giữ lại ERP)

| Màn | Quyền Xem | Thêm | Sửa | Xóa |
|---|---|---|---|---|
| model | Xem model | Thêm model | Sửa model | Xóa model |
| code đặt hàng | Xem code đặt hàng | Thêm code đặt hàng | Sửa code đặt hàng | Xóa code đặt hàng |
| đơn vị tính | Xem đơn vị | Thêm đơn vị | Sửa đơn vị | Xóa đơn vị |
| thuộc tính | Xem thuộc tính | Thêm thuộc tính | Sửa thuộc tính | Xóa thuộc tính |
| đơn vị thuộc tính | Xem đơn vị thuộc tính | Thêm đơn vị thuộc tính | Sửa đơn vị thuộc tính | Xóa đơn vị thuộc tính |
| thương hiệu | Xem thương hiệu | Thêm thương hiệu | Sửa thương hiệu | Xóa thương hiệu |
| hãng sản xuất | Xem hãng sản xuất | Thêm hãng sản xuất | Sửa hãng sản xuất | Xóa hãng sản xuất |
| xuất xứ | Xem xuất xứ | Thêm xuất xứ | Sửa xuất xứ | Xóa xuất xứ |
| file đính kèm | **KHÔNG có quyền nào** | — | — | — |
| mã màu | Xem danh sách mã màu | Thêm mã màu | Sửa mã màu | Xóa mã màu |
| thuế suất | Xem thuế suất | Thêm thuế suất | Sửa thuế suất | Xóa thuế suất |

⚠️ **8/11 quyền đang được màn `pi-*` của nhóm "Hàng hóa có sẵn" dùng CHUNG** (route
`pi-model.*`, `pi-units.*`, `pi-attributes.*`, `pi-uniteches.*`, `pi-brands.*`, `pi-barcodes.*`,
`pi-origins.*`, `pi-manufactures.*` — đều `checkPermission` cùng tên quyền). Nhóm đó **GIỮ LẠI
ERP** → **không được đổi tên, không được xoá** các quyền này.

⚠️ **Danh mục file đính kèm không gắn `checkPermission` ở bất kỳ route nào** — ai đăng nhập cũng
vào được. Port sang HRM phải quyết có tạo quyền mới hay không.

## 6. Bộ cột + bộ lọc từng màn (đọc từ blade / datatable JS)

| Màn | Cột danh sách | Ô lọc |
|---|---|---|
| model | Model · Trạng thái · Người cập nhật · Ngày cập nhật · Hành động | — |
| code đặt hàng | STT · Hãng sản xuất · Code đặt hàng · Ngày cập nhật · Người cập nhật · Hành động | — |
| đơn vị tính | STT · Tên · **Đơn vị cơ bản** · Trạng thái · Ngày cập nhật · Người cập nhật · Hành động | — |
| thuộc tính | STT · Tên thuộc tính · ~~Nhóm hàng hóa~~ (đã comment) · Trạng thái · Ngày cập nhật · Người cập nhật · Hành động | — |
| đơn vị thuộc tính | STT · Tên · Trạng thái · Ngày cập nhật · Người cập nhật · Hành động | — |
| thương hiệu | STT · Tên · Mã · Trạng thái · Ngày cập nhật · Người cập nhật · Hành động | Tên · Mã · Trạng thái · Người cập nhật (select-ajax) |
| hãng sản xuất | STT · Tên · Mã · Trạng thái · Ngày cập nhật · Người cập nhật · **Kế hoạch mua hàng** · **Đại diện hãng** · **Cấu hình** · Hành động | (chưa đọc hết) |
| xuất xứ | STT · Tên · **Vị trí** · Trạng thái · Ngày cập nhật · Người cập nhật · Hành động | — |
| mã màu | STT · Mã màu · Tên màu · Người lập · Ngày lập · Người sửa · Ngày sửa · Trạng thái · Hành động | — |
| thuế suất | STT · **% Thuế suất** · Trạng thái · Người cập nhật · Ngày cập nhật · Hành động | — |
| file đính kèm | (chưa đọc — controller không trả view thường) | — |

## 7. Import / Xuất / In — có sẵn ở ERP

| Màn | Import Excel | Xuất Excel | Xuất CSV | Xuất PDF | In |
|---|---|---|---|---|---|
| model | ✅ | — | — | — | — |
| code đặt hàng | — | — | — | — | — |
| đơn vị tính | ✅ | ✅ | ✅ | ✅ | — |
| thuộc tính | ✅ | ✅ | ✅ | ✅ | — |
| đơn vị thuộc tính | — | ✅ | ✅ | ✅ | — |
| thương hiệu | ✅ | ✅ | ✅ | ✅ | — |
| hãng sản xuất | ✅ | ✅ | ✅ | ✅ | — |
| xuất xứ | ✅ | ✅ | ✅ | ✅ | — |
| mã màu | — | ✅ | — | — | ✅ `printList` |
| thuế suất | — | ✅ | — | — | — |
| file đính kèm | — | — | — | — | — |

## 8. Màn nặng hơn danh mục thường

**Hãng sản xuất** không phải danh mục đơn. Ngoài CRUD còn:
- `Manufacture.kpiOrder` + `kpiOrder.searchData` + `kpiOrder.update` → màn **Kế hoạch mua hàng**
- `Manufacture.kpiSale` + `kpiSale.searchData` + `kpiSale.update` → màn **KPI bán hàng**
- `Manufacture.configEmployee` + `configEmployee.searchData` + `configEmployee.update` → màn **Cấu hình nhân viên**
- `Manufacture.getBuyer` / `getDeputy` → người mua hàng / người đại diện
- Cột nghiệp vụ riêng: `has_vat`, `represent_id`, 4 mốc thời gian `since_delivery_time` /
  `since_approved_time` / `since_PO_time` / `since_PI_time`
- Blade riêng: `kpi_order` · `kpi_sale` · `config_employee` · `export_excel` · `pdf`

**Đơn vị tính** có route riêng `unit.updateEnglishName` gắn quyền **`Tổng hợp đặt hàng`**
(không phải quyền đơn vị) — sửa tên tiếng Anh là chức năng của người làm đặt hàng.

## 9. Việc HRM đã chạm tới 2 trong 11 bảng

Phase 0 đã tạo 2 model **chỉ đọc**: `ErpAttribute` (`attributes`) và `ErpTaxRate` (`tax_rates`)
trong `Modules/MasterData/Entities/ProductClassification/`, phục vụ:
- `product_type_attributes` — pivot `product_types` ↔ `attributes`
- `product_types.vat_percent_tax_rate_id` → `tax_rates.id`

→ Phase 1 biến 2 bảng này thành **ghi được** bên HRM. Phải giữ nguyên `id`, và kiểm lại 2 màn
Phase 0 sau khi sửa.

## 10. Thứ tự phụ thuộc giữa 11 màn

- `barcodes.manufacture_id` **NOT NULL** → làm **Hãng sản xuất trước Code đặt hàng**.
- 9 màn còn lại độc lập nhau.
