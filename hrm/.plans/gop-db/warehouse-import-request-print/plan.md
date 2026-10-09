# Plan — Nút In màn chi tiết Đề nghị nhập kho mở popup xem trước theo SRS chung

Nguồn: user báo "Nút in tại màn chi tiết đề nghị nhập kho đang không hiển thị đúng popup in
theo srs chung" (2026-09-18).

## Bối cảnh / chẩn đoán
- FE `pages/finance/warehouse-import-requests/_id/index.vue` đang dùng `window.print()` (in
  cả trang trình duyệt), nút `secondary`, KHÔNG mở popup `ReportPrintPreviewModal` — SAI chuẩn
  print-page (LUẬT GỐC mục 0: nút In màn danh sách/chi tiết phải mở popup xem trước dùng chung).
- BE thiếu endpoint `GET finance/warehouse-import-requests/{id}/print-data` trả
  `{ data: { template } }` (HTML mẫu in ERP đã fill). Theo cây quyết định skill: BE thiếu →
  thêm BE từ mẫu in ERP rồi dựng popup. Màn tài chính port ERP KHÔNG có ngoại lệ trang `/print`.
- Mẫu in: `report_templates` id 45 "Phiếu đề nghị nhập kho" (đã verify erp_new) — 12 placeholder:
  LOGO, CONG_TY, DIA_CHI_CONG_TY, SO_PHIEU, PHIEU_YCNH, NGUOI_YEU_CAU, LOAI_NHAP, NGUOI_LAP,
  KHO_NHAP, NGAY_LAP, GHI_CHU, CHI_TIET. Đầu mẫu là bảng chứa `{{LOGO}}` (khớp regex
  `applyLetterheadHeader`) → dùng analog `ProductTransferRequestService` (LOGO-based letterhead).
- Letterhead theo `company_id` GHI TRÊN CHỨNG TỪ (warehouse_import_requests CÓ cột company_id),
  fallback công ty người tạo — theo `BillIncomePrintService::headerUrl()` (CLAUDE.md letterhead).

## Task
### BE (hrm-api)
- [x] `WarehouseImportRequestService`: thêm `const PRINT_TEMPLATE_ID = 45` + `printData()` +
      `buildPrintData()` (12 placeholder) + `buildPrintProductTable()` (bảng phẳng, field
      `model_name`, `formatCurrency(qty,2)`) + `applyLetterheadHeader()` + `resolvePrintCompany()`
      resolve company theo `$model->company_id` (fallback creator). Escape `e()` text, `addcslashes`
      trước `fillReport`.
- [x] `WarehouseImportRequestController::printData($id, WarehouseImportRequestService $service)` —
      per-method injection, guard bằng `scopedQuery()` (404 nếu ngoài quyền), 404 nếu thiếu mẫu.
      Trả `responseJson('success', 200, ['template' => $html])`.
- [x] Route `GET /{id}/print-data` khai TRƯỚC `/{id}` trong nhóm `/warehouse-import-requests`.

### FE (hrm-client)
- [x] `pages/finance/warehouse-import-requests/_id/index.vue`: import + mixin
      `reportPrintPreviewMixin` + component `ReportPrintPreviewModal`, thêm phần tử modal bind
      `printPreview`, nút In `secondary`→`primary size="sm"`, `printDetail()` → `openPrintDetail(
      'finance/warehouse-import-requests', this.id, 'Xem trước phiếu đề nghị nhập kho')`, bỏ
      wrapper `#print-area` + block `@media print` (không còn window.print). Giữ LF.

### Verify
- [x] Playwright 127.0.0.1:3000: mở chi tiết ĐNNK PDNNK-01886 (id 1886), bấm In → popup xem trước
      dùng chung `ReportPrintPreviewModal` mở tại chỗ, tiêu đề "Xem trước phiếu đề nghị nhập kho",
      render đủ mẫu 45 đã fill (letterhead img, No: PDNNK-01886, PYCNH-03111, người yêu cầu, bảng
      CHI_TIET STT/Tên hàng hóa/Model/Mã hàng hóa/Thương hiệu/Số lượng/Đơn vị tính), KHÔNG còn
      placeholder `{{ }}`. Screenshot: `hrm-client/dnnk-print-popup-1886.png`.

## Checkpoint
### Checkpoint — bắt đầu (2026-09-18)
Vừa hoàn thành: chẩn đoán FE+BE, verify template 45 (12 placeholder, LOGO-based), chốt analog.
Đang làm: viết BE service/controller/route + FE popup.
Bước tiếp theo: verify Playwright.
Blocked: không

### Checkpoint — XONG toàn bộ + verify UI (2026-09-18)
Vừa hoàn thành: cả BE + FE + verify thật trên trình duyệt.
- BE: `WarehouseImportRequestService` (PRINT_TEMPLATE_ID=45 + printData + buildPrintData 12
  placeholder + buildPrintProductTable + applyLetterheadHeader + resolvePrintCompany + headerUrl/
  erpAssetUrl), `WarehouseImportRequestController::printData()`, route `GET /{id}/print-data`.
  `php -l` sạch cả 3 file. Smoke test tinker (WIR 9806): HTML 2623 ký tự, không còn `{{`, letterhead
  img đúng (ghép ERP_URL vào companies.header của company_id trên chứng từ).
- FE: `_id/index.vue` — import + mixin `reportPrintPreviewMixin` + component
  `ReportPrintPreviewModal`, thêm phần tử modal bind `printPreview.*`, nút In đổi `secondary`→
  `primary size="sm"`, `printDetail()` gọi `openPrintDetail('finance/warehouse-import-requests',
  this.id, 'Xem trước phiếu đề nghị nhập kho')`, bỏ wrapper `#print-area` + block `@media print`
  (hết `window.print`). File giữ LF (grep `\r` = 0).
- Verify Playwright (DNS Admin, PDNNK-01886 / id 1886): bấm In → popup `ReportPrintPreviewModal`
  mở tại chỗ đúng chuẩn SRS chung, render đủ mẫu đã fill (letterhead img + toàn bộ placeholder +
  bảng CHI_TIET đúng 7 cột), không còn `{{ }}`. Screenshot lưu ở
  `hrm-client/dnnk-print-popup-1886.png`.
Bước tiếp theo: xong task. CHƯA commit/push (chờ user yêu cầu).
Blocked: không
