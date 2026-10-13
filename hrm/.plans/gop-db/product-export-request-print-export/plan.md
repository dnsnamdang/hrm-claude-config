# Plan — 3 chức năng In/Xuất Excel Yêu cầu xuất hàng

## Phase 1 — Function 1: In yêu cầu (mẫu ERP report_templates id 13)
- [x] BE: `ErpReportTemplate::YEU_CAU_XUAT_HANG = 13`
- [x] BE: `ProductExportRequestPrintService` (fill mẫu 13: info + product_table 9 cột + footer suy line-sum)
- [x] BE: `ProductExportRequestController::printData($id)` (dùng scopedQuery + snapshot details)
- [x] BE: route `GET /{id}/print-data` (trước `/{id}`)
- [x] FE: nút "In yêu cầu" trong menu ⚙ + `reportPrintPreviewMixin.openPrintDetail`
- [x] Verify Playwright popup xem trước

## Phase 2 — Function 3: Xuất excel danh sách hàng (Bkav 22 cột)
- [x] BE: `ProductExportRequestBkavExport` (FromView) + blade Bkav 22 cột
- [x] BE: `exportProductList($id)` → download `{code}_Phieu_xuat_kho_kiem_van_chuyen_noi_bo.xlsx`
- [x] BE: route `GET /{id}/export-product-list`
- [x] FE: nút "Xuất excel danh sách hàng" (tải trực tiếp qua blob + auth)
- [x] Verify file tải về đúng cột/định dạng số

## Phase 3 — Function 2: In biên bản giao nhận - bàn giao (print_templates type 12)
- [x] BE: `ErpPrintTemplate` (bảng `print_templates`)
- [x] BE: `handoverTemplates()` — list mẫu type 12
- [x] BE: `ProductExportRequestHandoverPrintService` (fill mẫu + 4 biến thể bảng chi tiết)
- [x] BE: `printHandoverData($id, Request)` (5 tham số) + route `GET /{id}/print-handover-data`
- [x] FE: popup chọn mẫu + nhập người nhận (V2BaseModal + V2BaseSelectInModal) + nút menu ⚙
- [x] Verify Playwright popup + bản in

## Checkpoint
### Checkpoint — bắt đầu (2026-09-18)
Vừa hoàn thành: research đầy đủ (placeholder mẫu 13, union type 12, map handover accessor, 4 bảng chi tiết, Bkav 22 cột, điểm chèn controller/route/FE).
Đang làm dở: bắt đầu code Phase 1.
Bước tiếp theo: thêm const + service + controller + route + FE cho Function 1.
Blocked:

### Checkpoint — Phase 1 XONG (2026-09-18)
Vừa hoàn thành: Function 1 "In yêu cầu" trọn vẹn BE+FE.
- BE: const 13, `ProductExportRequestPrintService::render()`, `printData()` (scopedQuery), route `GET /{id}/print-data` — cả 3 file php lint sạch.
- FE: `pages/finance/product-export-requests/index.vue` — nút "In yêu cầu" (`ri-printer-line`) trong `#cell-action`, mixin `reportPrintPreviewMixin`, import+register `ReportPrintPreviewModal` + markup, `goPrint()` gọi `openPrintDetail('assign/product-export-requests', id, ...)`.
- Verify Playwright (127.0.0.1:3000): 20 dòng → 20 nút In; click → popup `.report-print-modal` mở, title đúng, html 5749 ký tự, không lỗi. Bản in đầy đủ: header cty, mọi field KH/HĐ, bảng 9 cột, footer đủ nhánh (kiểm cả ca CÓ Giảm giá PYCXH-40338: 500,000→giảm 25,000→trước thuế 475,000→VAT 38,000→sau thuế 513,000, số định dạng quốc tế). Verify xong đã HOÀN TÁC quyền test tạm (role_has_permissions perm 100870/role 18/cty 1) — DB sạch.
Bước tiếp theo: Phase 2 — Function 3 (Bkav 22 cột excel): export class + blade + `exportProductList` + route + nút FE.
Blocked: không

### Checkpoint — Phase 2 XONG (2026-09-18)
Vừa hoàn thành: Function 3 "Xuất excel danh sách hàng" (Bkav 22 cột) trọn vẹn BE+FE + verify.
- BE: `Modules/Assign/Export/ProductExportRequestBkavExport.php` (FromView + WithColumnWidths; DonGia = price+extra_price mirror mẫu 13; ThanhTien = DonGia×SL; 3 ô số SoLuong/DonGia/ThanhTien = SỐ THẬT + data-format `#,##0`), blade `resources/views/exports/assign/product_export_request_bkav.blade.php`, `exportProductList($id)` (scopedQuery + join tên cty theo người lập + `$safeCode`), route `GET /{id}/export-product-list` (sau print-data, trước show). PHP lint sạch.
- FE: `pages/finance/product-export-requests/index.vue` — nút "Xuất excel danh sách hàng" (`ri-file-excel-2-line`) trong `#cell-action` (thứ tự: In yêu cầu → Xuất excel → Lịch sử), `exportProductList(item)` gọi `downloadExcel(...)`.
- Verify Playwright (127.0.0.1:3000): 20 dòng → 20 nút Xuất excel; click nút dòng PYCXH-40338 → tải đúng file `PYCXH-40338_Phieu_xuat_kho_kiem_van_chuyen_noi_bo.xlsx`. Đọc lại file bằng PhpSpreadsheet: 22 header đúng thứ tự, dòng note A1, ô G/H/I kiểu SỐ [n] fmt `#,##0` (SL 1 · ĐG 500,000 · TT 500,000), tên cty ở Cua/XuatKhoTai, VeViec "Vận chuyển hàng hóa", bề rộng cột A–V khớp. Endpoint trả 200 + content-type spreadsheet + magic `504b0304`. Đã HOÀN TÁC quyền test tạm (role_has_permissions perm 100870/role 18/cty 1) — DB sạch, file test đã xóa.
- Gotcha ghi nhớ: list rỗng khi thiếu quyền là do `Employee::roles` (spatie morphToMany) lọc `model_type` = `Modules\Timesheet\Entities\Employee` → chỉ role 18 (cty 1) tính; role 100002/100010 (`App\Employee`) bị loại. Muốn thấy data phải cấp perm cho ĐÚNG role 18.
Bước tiếp theo: Phase 3 — Function 2 (In biên bản giao nhận - bàn giao, print_templates type 12).
Blocked: không

### Checkpoint — Phase 3 XONG (2026-09-18) — TOÀN BỘ FEATURE HOÀN THÀNH
Vừa hoàn thành: Function 2 "In biên bản giao nhận - bàn giao" (print_templates type 12) trọn vẹn BE+FE + verify.
- BE (đã có sẵn, lint sạch): `ErpPrintTemplate` (bảng `print_templates`), `handoverTemplates()` (list mẫu type 12), `handoverEmployees()` (nhân viên cùng cty người lập, format `Tên - Mã phòng - Mã NV`), `ProductExportRequestHandoverPrintService` (fill mẫu + 4 biến thể bảng chi tiết), `printHandoverData($id, Request)` nhận 5 tham số, 3 route `GET /{id}/handover-templates | handover-employees | print-handover-data`.
- FE: `pages/finance/product-export-requests/components/HandoverPrintModal.vue` (V2BaseModal + V2BaseSelectInModal, 5 trường, chỉ THU THẬP tham số → `@preview`), `index.vue` nút "In biên bản giao nhận" (`ri-file-list-3-line`) + `openHandoverPrint`/`onHandoverPreview` (gọi server + mở lại `ReportPrintPreviewModal`).
- Verify Playwright (127.0.0.1:3000) trên PYCXH-40338: (a) modal mở đúng tiêu đề + subtitle "Phiếu: PYCXH-40338" + 5 trường; (b) select "Chọn biên bản" nạp 8 mẫu type 12 (SƠ BỘ/ĐÃ NGHIỆM THU/...); (c) select "Nhân viên đại diện" nạp 394 NV đúng format; (d) bấm In khi rỗng → hiện đủ 4 lỗi bắt buộc (template + người nhận + chức vụ + SĐT), employee_id KHÔNG bắt buộc; (e) điền hợp lệ + chọn mẫu 160 → In → `@preview` phát đúng payload → `ReportPrintPreviewModal` render bản in thật "BIÊN BẢN BÀN GIAO THIẾT BỊ SƠ BỘ" (html 10664 ký tự, có số HĐ, thông tin BÊN A/BÊN NHẬN, và các giá trị người nhận đã nhập).
- Đã HOÀN TÁC quyền test tạm (`role_has_permissions` perm 100870/role 18/cty 1 — deleted 1, remaining 0) + flush Spatie cache → DB sạch, hành vi phân quyền production khôi phục.
Bước tiếp theo: KHÔNG còn — cả 3 chức năng đã xong & verify. Chờ yêu cầu mới. (Chưa commit/push theo ràng buộc.)
Blocked: không
