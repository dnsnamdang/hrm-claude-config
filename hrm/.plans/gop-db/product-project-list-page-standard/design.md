# Chuẩn hoá màn Danh sách hàng hoá làm dự án theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/product-project`
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-product-project-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project`

## Đặc thù của màn này (khác 18 màn trước)

Dữ liệu **không đến từ một bảng**: là `UNION` giữa `bom_list_products` (BOM tổng hợp đã duyệt) và
`quotation_product_prices` (báo giá tự lập đã duyệt / trúng thầu), lọc bỏ hàng ERP gốc, **gộp trùng
mã trong PHP**, rồi mới phân trang bằng `LengthAwarePaginator`. Hệ quả:

- Không có Entity / Resource → cột xuất file khớp mảng của `ProductProjectController::transformItem()`.
- Sắp xếp **không làm bằng SQL** mà trên collection đã gộp, trước khi phân trang.
- Màn **CHỈ ĐỌC**: không Tạo / Sửa / Xóa / Khoá (routes chỉ có `index`, `export` và các endpoint
  phục vụ picker) → **không có cột Hành động**, và cột Mã hàng **không phải link** (không có màn chi
  tiết cho hàng hoá dự án). Lối vào chứng từ nguồn nằm ở cột **Mã BOM**.

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (7 ô), bỏ `title`/`subtitle`, placeholder
   theo công thức "Chọn <trường>", ô gõ tay chờ Enter (`textFilterKeys`).
2. Bảng: bật `fixed-layout`, **17 cột đều khai `width` = `minWidth`** theo 4 bậc, đo trên **181 dòng
   thật của chính màn**; ô tham chiếu (Dự án · Giải pháp · Hàng hoá cha) ghép `MÃ - Tên` cùng 1 dòng.
3. Thêm cột **Ngày tạo** (trước chỉ có Người tạo); Trạng thái đồng bộ dùng `V2BaseBadge` + màu BE trả.
4. `columnCustomizationMixin` + popup **Chọn trường xuất file** (`exportFieldsMixin` +
   `ExportColumnRegistry` + `DynamicExport`, `.xls` → `.xlsx`).
5. BE: whitelist sắp xếp (Mã hàng / Tên hàng / Ngày tạo — trước `sort_field` bị **bỏ qua hoàn toàn**),
   chốt `row_id desc` để phân trang ổn định; thêm `erp_sync_status_color`; thêm
   `product_attributes_text` (hạ HTML về chữ) cho file Excel.
6. Bỏ sạch `'—'`, bỏ in đậm trong ô, xoá CSS chết (`.pp-chip`, `.pp-code-badge`, `.pp-icon-btn`).

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột Hành động | **Không có** — màn chỉ đọc, không có thao tác nào để đặt vào |
| Cột định danh | **Mã hàng**, chữ thường (không link — không có màn chi tiết) |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Chưa làm** — module Assign chưa có `LogsCatalogHistory` |
| TSKT trong file Excel | Dùng `product_attributes_text`, các dòng nối bằng " · " |

## File chính

- BE: `Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `hrm-client/pages/assign/product-project/index.vue`

Không migration, không quyền mới.
