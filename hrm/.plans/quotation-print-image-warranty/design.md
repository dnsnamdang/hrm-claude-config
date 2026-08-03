# Cột "Hình ảnh" + "Thời gian bảo hành" cho In / Xuất Excel báo giá

@khoipv · bắt đầu 2026-07-18

## Mục tiêu
Bổ sung 2 cột tuỳ chọn **Hình ảnh** và **Thời gian bảo hành** vào popup "Cấu hình in báo giá",
áp dụng cho cả **bản in (preview)** và **file Xuất Excel** (`BaoGia_*.xlsx`).

Màn: Phân hệ Dự án TKT → chi tiết báo giá (`/assign/quotations/{id}`), popup Cấu hình in.

## Quyết định đã chốt (user)
- **Nguồn dữ liệu**: lấy live từ **ERP qua connection `mysql2`** (bảng `products`) theo `erp_product_id`.
  - Ảnh = `products.avatar` (URL S3 đầy đủ).
  - Bảo hành = `products.guarantee` + `products.guarantee_type` (`thang`/`ngay`/`nam`) → "X tháng/ngày/năm".
  - Hàng khai tay (không `erp_product_id`) → để trống.
- **Phạm vi**: cả bản In và Xuất Excel.
- **Mặc định**: 2 checkbox **tích sẵn** khi mở popup.
- **Ảnh trong Excel**: **nhúng ảnh thật** (WithDrawings, pattern như export nhân viên).
- **Thứ tự cột**: ... → Thành tiền sau VAT → **Hình ảnh** → **Thời gian bảo hành** (2 cột cuối).

## Kiến trúc / điểm chạm
- **Bản in**: FE thuần + BE resource.
  - `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue`: +2 cột `image`,`warranty`.
  - `hrm-client/components/assign/quotation/QuotationPrintPreview.vue`: render 2 cột + chờ ảnh load rồi mới in.
  - `hrm-api/Modules/Assign/Transformers/DetailQuotationResource.php`: batch mysql2 enrich `image`+`warranty` (2 nhánh direct/BOM).
- **Xuất Excel** (nút "Xuất Excel" → `QuotationController::exportExcel` → `App\ExcelExport\BomListExport`, file `BaoGia_*.xlsx`; KHÔNG phải file import round-trip):
  - `exportExcel`: enrich `image_url`+`warranty` cho `$bom->products` (cùng batch mysql2) + thêm `image`,`warranty` vào `defaultFields`.
  - `resources/views/exports/bom_list.blade.php`: +2 cột (header + mọi biến thể dòng + footer colspan).
  - `app/ExcelExport/BomListExport.php`: width cột + nhúng ảnh (WithDrawings) neo theo dòng.

## Không đụng
- KHÔNG sửa chức năng Import (Import map theo tên header, bỏ qua cột lạ — đã verify).
- KHÔNG sửa `QuotationExcelExport` (file round-trip riêng, route `export-quotation-data`).
- KHÔNG migration/permission/git.

## AC
- AC1: popup có đủ 2 tuỳ chọn tích/bỏ tích Hình ảnh + Thời gian bảo hành.
- AC2: tích cả 2 → bản in hiện đủ 2 cột kèm dữ liệu.
- AC3: bỏ cả 2 → ẩn 2 cột, bảng tự co giãn cân đối.
- AC4: tích 1 trong 2 → hiện đúng cột chọn, ẩn cột kia.

Spec chi tiết: `docs/superpowers/specs/2026-07-18-quotation-print-image-warranty-design.md`
