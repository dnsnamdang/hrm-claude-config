# Design — Bổ sung 4 chức năng màn "Danh sách đề nghị xuất kho"

Redmine: **[ERP => HRM] Đề nghị xuất kho - Danh sách - Thiếu chức năng** (Nguyễn Minh Hằng → Trần Cư,
Mới, Cao, start 09/09/2026). URL: http://hrm-crm.eteksofts.com/finance/warehouse-export-requests.
Mô tả verbatim: **"Thiếu chức năng Cài đặt bộ lọc, Xuất excel danh sách, In bộ giấy tờ đi đường,
In đề nghị"**.

Màn HRM: `hrm-client/pages/finance/warehouse-export-requests/index.vue` (đề nghị xuất kho — ĐNXK,
module Assign). Đây là màn danh sách đã port sẵn nhưng **thiếu 4 chức năng** trên.

## Nguyên tắc

- Khuôn chuẩn trong project: màn **`product-export-requests`** (STATUS `product-export-request-print-export`
  đã port đúng 3 chức năng In yêu cầu / Xuất excel danh sách hàng / In biên bản giao nhận) +
  màn "Danh mục khách hàng" (mẫu gốc erp-to-hrm-screen). Copy pattern, KHÔNG bê UI ERP.
- ERP = nguồn nghiệp vụ; HRM = nguồn giao diện. Print HRM dùng `*PrintService::render()` + blade +
  `ReportPrintPreviewModal`, KHÔNG dùng `report_templates` HTML của ERP.

## Khảo sát ERP (Bước 1 — đã xong)

Nguồn ERP: `app/Http/Controllers/Warehouse/WarehouseExportRequestsController.php`,
model `app/Model/Warehouse/WarehouseExportRequest.php`, routes `routes/web.php:1200-1217`.

### 1. Cài đặt bộ lọc (filter)
9 trường lọc + time range + company/department (ERP `search_columns` + `searchByFilter`):
`product_name` (tên/mã hàng) · `code` (mã phiếu) · `export_type` (loại) · `product_export_request`
(mã YCXH) · `requester` (người yêu cầu) · `created_by` (người lập) · `customer` (khách hàng) ·
`status` (1–7) · `approver` (người duyệt) · `startDate`/`endDate` (ngày lập) · `company`/`department`.
→ HRM hiện dùng `V2BaseFilterPanel` + slot `#advanced-filters` (THIẾU popup "Cài đặt bộ lọc").
   Phải chuyển sang **`V2BaseSmartFilterPanel` + schema `filterFields`** (bật `floating`).

### 2. Xuất excel danh sách (toolbar)
ERP `exportList` re-run `searchByFilter($request)->get()` (cùng filter với danh sách), 12 cột:
STT · Mã phiếu · Loại · Phiếu YCXH · Khách hàng · Người yêu cầu · Người lập · Ngày lập · Trạng thái ·
Người duyệt · Ngày nhận · Ngày duyệt. (≥2000 dòng thì ERP email; HRM theo skill list-page 14c.)
→ HRM: nút toolbar "Xuất Excel" (secondary success `ri-file-excel-2-line`) → `ExportFieldsModal`
   (chọn trường) → BE `GET .../export` trả JSON theo filter → dựng file ở FE bằng ExcelJS.

### 3. In bộ giấy tờ đi đường (row action, printMove) — ⚠️ QUYẾT ĐỊNH PENDING
ERP `printMove($id)` render 1 BỘ tài liệu cho 1 phiếu:
  - **Lệnh điều động** (`ReportTemplate::LENH_DIEU_DONG=55`) — luôn có, từ `print_move_data`.
  - **Phiếu xuất kho đi đường** (`PHIEU_XUAT_KHO_DI_DUONG=59`) — CHỈ khi `warehouse_id` có giá trị.
  - (tuỳ chọn) PDF `attachment_passport` của công ty người lập.
Render qua `printMulti.blade.php` (nhiều template + PDF nhúng trên 1 trang).
→ KHÁC với "In biên bản giao nhận" của product-export (chọn mẫu + người nhận). Cần chốt cách port
   sang HRM — xem "Quyết định cần chốt" #1.

### 4. In đề nghị (row action, print)
ERP `print($id)` render 1 template **Đề nghị xuất kho** (`ReportTemplate::DE_NGHI_XUAT_KHO=14`) từ
`print_data`: header công ty, số HĐ, số phiếu, ngày xuất, loại, KH + liên hệ + SĐT, địa chỉ giao,
người yêu cầu, người lập, phòng ban, ghi chú + bảng hàng hoá (STT/Tên/Model/Mã/Thương hiệu/ĐV/SL + tổng).
→ HRM: nút row "In đề nghị" (`ri-printer-line`) → `reportPrintPreviewMixin.openPrintDetail` →
   BE `GET .../{id}/print-data` → `WarehouseExportRequestPrintService::render()`.

### Điều kiện hiện/ẩn row action (ERP, ngoài 4 chức năng nhưng cùng dòng)
Sửa/Hủy/Tạo phiếu xuất kho/Tạo phiếu điều chuyển — HRM đã có Sửa/Hủy/Tạo phiếu xuất kho. In đề nghị
và In giấy tờ đi đường là **thao tác chỉ đọc** → luôn hiện (không gate quyền ghi).

## Quyết định cần chốt (trước khi code)

1. **"In bộ giấy tờ đi đường"** — port bộ 2 tài liệu (Lệnh điều động + Phiếu xuất kho đi đường) thế nào:
   (A) 1 nút "In giấy tờ đi đường" → `ReportPrintPreviewModal` render CẢ 2 tài liệu (mỗi tài liệu 1
       trang giấy), Phiếu xuất kho đi đường chỉ chèn khi `warehouse_id` có — **đề xuất**;
   (B) modal nhỏ cho user chọn in tài liệu nào;
   (C) mirror pattern handover (chọn mẫu + người nhận) như product-export.
   → PDF `attachment_passport`: HRM có trường tương đương không (cần kiểm `companies`)? Nếu không, bỏ.

2. **Dọn vi phạm quy ước sẵn có khi rework file** (ô rỗng `—` → để trống; `$bvModal.msgBoxConfirm`
   → `$confirm()`; `font-weight-bold` cột Mã → bỏ): làm luôn (đề xuất) hay giữ nguyên?

## Quyết định đã chốt

1. **"In bộ giấy tờ đi đường" = hướng A + A1** (user chốt "theo bạn" — 18/09/2026):
   - 1 row-action **"In giấy tờ đi đường"** (`ri-printer-line`) → `reportPrintPreviewMixin` +
     `ReportPrintPreviewModal`. BE endpoint riêng `GET .../{id}/print-move-data` →
     `WarehouseExportRequestMovePrintService::render()` trả HTML gồm:
     - **Lệnh điều động** (blade riêng, luôn render) — dữ liệu từ `print_move_data` của ERP model.
     - **Phiếu xuất kho đi đường** (blade riêng) — CHỈ nối thêm khi phiếu có `warehouse_id`
       (từ `print_pxk_data`). Mỗi tài liệu 1 tờ A4, nối tiếp bằng page-break.
   - **BỎ passport PDF** ở bản in HRM (A1). `companies.attachment_passport` CÓ trong DB gộp nhưng
     preview HRM là HTML blade, nhúng PDF ngoài vào giữa luồng in rất vướng; passport vốn optional
     (`?? null` ở ERP). Có thể bổ sung link tải riêng sau nếu user cần.
2. **Dọn vi phạm quy ước liền kề: LÀM LUÔN** khi rework file (ô rỗng `—`→trống, cột Mã bỏ bold +
   nuxt-link, `$bvModal.msgBoxConfirm`→`$confirm()`, thêm `columnCustomizationMixin`).
