# Port 3 chức năng In/Xuất Excel cho màn Yêu cầu xuất hàng (HRM)

**Người phụ trách:** @namdangit
**Nhánh:** `gop_db` (cả hrm-api + hrm-client)
**Màn HRM:** `/finance/product-export-requests` (Module Assign — API prefix `assign/product-export-requests`)
**Màn ERP nguồn:** `/admin/warehouse/product_export_requests?type=all`

## Mục tiêu

Trên ERP, mỗi bản ghi "Danh sách yêu cầu xuất hàng" có menu ⚙ với 3 chức năng mà HRM chưa có:

1. **In yêu cầu** — bản in Phiếu yêu cầu xuất hàng (mẫu ERP `report_templates` id **13**).
2. **In biên bản giao nhận - bàn giao** — bản in biên bản (mẫu ERP `print_templates` type **12**, chọn mẫu + nhập người nhận trong popup).
3. **Xuất excel danh sách hàng** — file Bkav 22 cột (`{code}_Phieu_xuat_kho_kiem_van_chuyen_noi_bo.xlsx`).

Yêu cầu gốc: "Trên erp bản ghi đang có 2 chức năng in và 1 chức năng xuất excel. HRM chưa có => Thêm đầy đủ." User chốt **"làm luôn"** — làm đủ cả 3.

## Kiến trúc (mirror pattern đã nghiệm thu của Phiếu xuất hàng)

- **In**: popup xem trước qua `reportPrintPreviewMixin` (FE) + BE trả `{ data: { template: '<html>' } }`.
  BE fill mẫu ERP bằng `fillReport()` + `clearNull()` (placeholder `{{KEY}}`, thay GLOBAL, escape `$`/`\` bằng `addcslashes`).
  Khuôn mirror: `ProductExportPrintService` (Phiếu xuất hàng, mẫu 48) + `ProductExportController::printData()`.
- **Xuất Excel Bkav**: BE `maatwebsite/excel` (FromView) + blade — mirror ERP `ProductExportRequestDetailExport` + blade
  `reports/exports/product_export_request_detail_report.blade.php`. Tải trực tiếp (không qua popup xem trước).
- **Nguồn số liệu**: bảng snapshot `product_export_request_details` (cùng nguồn `show()` của controller) — 3 chức năng
  đều dựng từ bảng này, KHÔNG cần model ERP.

## Quyết định đã chốt

- **Logo/công ty đầu phiếu**: lấy theo **người tạo phiếu** (`created_by` → `employees.employee_info_id` →
  `employee_infos.company_id` → `companies`), y hệt `ProductExportPrintService::company()` (đã nghiệm thu) và đúng
  ERP `getPrintDataAttribute()` (dùng `employee_create->info->company`). Giữ nhất quán 2 bản in cùng màn.
- **Function 1 — `THONG_TIN_THANH_TOAN_HOP_DONG` = rỗng** cho màn HRM: accessor ERP `contract_payment_table` chỉ
  sinh bảng cho loại 1 (xuất hàng thường) / 2 (KM) / dịch vụ; HRM xử lý loại 19/20/21 → accessor trả '' → placeholder
  để trống (`clearNull` xoá). Parity đúng cho các loại màn này.
- **Function 1 — product_table (9 cột)**: STT · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu · ĐV · SL · Đơn giá ·
  Thành tiền. Đơn giá = `price + extra_price` (giá bán sau phụ thu); Thành tiền = qty × Đơn giá. Footer suy từ line-sum
  (mirror `paymentSummary` FE detail): Tổng cộng = Σ qty×(price+extra); Giảm giá = Σ(price+extra−allocated)×qty (hiện
  nếu ≠0); Tổng tiền trước thuế = Σ qty×allocated (hiện nếu có allocated); Tiền VAT = Σ round(qty×allocated×vat/100)
  (hiện nếu >0); Tổng tiền sau thuế = trước thuế + VAT. SL/qty format `formatCurrency($x,3)` (HRM không có
  `formatQuantity`); tiền `formatCurrency($x)`. Số theo chuẩn quốc tế `1,234,567.89`.
- **Function 2 — 4 biến thể bảng chi tiết** dựng từ `product_export_request_details`: không giá 6 cột · không giá +
  serial 7 cột · có giá 8 cột · có giá + serial 9 cột. Xuất xứ lấy `products.origin_id` → `origins.name` (guard null).
  Cột Serial để trống. Footer có-giá dùng nhánh phổ biến (Tổng cộng thanh toán = Σ qty×đơn-giá; "Bằng chữ" qua
  `convertNumberToWords()` — HRM CÓ hàm này ở `app/Helper/FormatHelper.php:201`).
- **Function 2 — mẫu type 12**: đọc bảng dùng chung `print_templates` (KHÔNG phải `hrm_print_templates`) qua model mới
  `ErpPrintTemplate`. Popup chọn 5 tham số: `template_id` (bắt buộc), `employee_id` (đại diện bên giao, tùy chọn),
  `employee_receiver` (bắt buộc), `role_name` (bắt buộc), `telephone` (bắt buộc).
- **Function 3 — Bkav 22 cột**: mirror `getProductTableExportAttribute` ERP; cờ `HEADER_FILE_IMPORT_INVOICE=1` bỏ dòng
  tiêu đề. Tải trực tiếp file.
- **DB**: `product_export_requests` KHÔNG có `invoice_export_address` → dùng `customer_address`. `products.origin_id` có.
  `companies` có name/phone/address/logo/header/fax.

## Endpoints (đều đặt TRƯỚC route `/{id}`)

| Chức năng | Method + path | Controller |
|---|---|---|
| 1. In yêu cầu | `GET /{id}/print-data` | `printData()` |
| 2. Danh sách mẫu type 12 | `GET /handover-templates` | `handoverTemplates()` |
| 2. In biên bản giao nhận | `GET /{id}/print-handover-data` (query 5 tham số) | `printHandoverData()` |
| 3. Xuất excel danh sách hàng | `GET /{id}/export-product-list` | `exportProductList()` |

## File thay đổi

**hrm-api**
- `Modules/Finance/Entities/ErpReportTemplate.php` — thêm `const YEU_CAU_XUAT_HANG = 13;`
- `Modules/Assign/Entities/ErpPrintTemplate.php` — MỚI (bảng `print_templates`).
- `Modules/Assign/Services/ProductExportRequestPrintService.php` — MỚI (Function 1).
- `Modules/Assign/Services/ProductExportRequestHandoverPrintService.php` — MỚI (Function 2).
- `Modules/Assign/Export/ProductExportRequestBkavExport.php` — MỚI (Function 3, FromView).
- `Modules/Assign/Resources/views/exports/product_export_request_bkav.blade.php` — MỚI (blade Bkav).
- `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` — thêm 4 method.
- `Modules/Assign/Routes/api.php` — thêm 4 route (trước `/{id}`).

**hrm-client**
- `pages/finance/product-export-requests/index.vue` — thêm 3 nút menu ⚙ + popup handover + `reportPrintPreviewMixin`.
- Popup handover: component mới (V2BaseModal + V2BaseSelectInModal).
