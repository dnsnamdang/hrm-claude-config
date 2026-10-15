# Plan đợt C-c — lỗi cũ ERP (việc ngoài luồng) — 13/10/2026

> Nguồn: `cc-khao-sat.md` (khảo sát + chốt C-c-1). N47/N48 bỏ qua (user 13/10).
> ✅ User "làm" 13/10.
> ERP worktree `wt-erp-2d1` — nhánh con `feat/cc-loi-cu-erp` từ `feat/2d1-erp-khong-loi`. DB `hrm_erp_giacty`.

## Task ERP
- [x] E1 N46 `warehouse/warehouse_imports/barcode.blade.php`: thêm `@include('partials.classes.warehouse.WarehouseImportArrangeDelivery')` trước `WarehouseImport`.
- [x] E2 N41 `ProductsController::barcode()`: nhánh `twoCode == 'false'` (Mẫu 1) chỉ in hàng `(int) barcode_template_type !== 2`; sửa chú thích 2-D1.
- [x] E3 N43 xoá `App\Model\ProductInfo\BaseProduct::isRequiredSeri()` (gọi class không tồn tại, không ai gọi).
- [x] E4 N44 (C-c-1 + C-c-2 — gỡ HẾT xuất ở màn Danh sách hàng hoá ERP, HRM làm lại sau): `products/list.blade.php` bỏ nút "Xuất Excel" + modal `#columnExportSetting` + JS `columnExportSetting/applyExportColumnSetting` + nút "Hàng chưa có công khoán" + 3 dòng comment CSV/Excel/PDF + handler `.export-button` nếu không còn ai dùng; `routes/web.php` gỡ 5 route `products.exportExcel|exportCSV|exportPDF|exportExcelNorm|exportProduct` (kiểm `route('…')` khác trỏ tới trước khi gỡ); `ProductsController` gỡ 5 action + import thừa; `App\Product::exportExcel()` xoá. GIỮ class ProductReportExport/Norm + ProductMailJob (controller cũ còn tham chiếu). Nếu `products/pdf.blade.php` chỉ phục vụ exportPDF ⇒ xoá.
- [x] E5 N45 `tests/Feature/ExampleTest`: chưa đăng nhập vào `/` ⇒ chuyển hướng (302), không 500.
- [x] E6 N49 `partials/modals/js/calculateDeliveryCost.blade.php` `handleSelectPayload` (+ `handleSelectVehicle` cùng kiểu): `success === false` ⇒ toastr báo `message`, xoá cost/km cũ (khuôn thông báo lỗi đang dùng ở ERP); không đổi `ResponseTrait`.
- [x] E7 N50 `partials/classes/sale/QuotationTemplate.blade.php`: getter `products` (+ getter mảng khác cùng kiểu trong file) gán `[]` 1 lần, trả cùng tham chiếu.
- [x] E8 N51 `products/formShow.blade.php:923`: bỏ `function` khỏi biểu thức Angular — chuỗi NCC tính ở controller; đo lại bố cục khối chi tiết hàng hoá.
- [x] E9 Test: PHPUnit ERP (ca mới: barcode Mẫu 1 lọc mẫu 2; 5 route xuất đã gỡ ⇒ không còn trong route list) + cả bộ.

## Tài liệu
- [x] D1 N39 `hrm-claude-config/erp/CLAUDE.md` Tech Stack: "Laravel 6 (`^6.2`, đang cài 6.20.45)".

## Kiểm (Playwright MCP, ERP 8090 — role tạm, gỡ khi xong)
- TÁI HIỆN TRƯỚC khi sửa: N46 màn in tem PNK trống + ReferenceError; N49 `reading 'cost'` (công ty chưa có bảng giá vận chuyển / tuyến không khớp); N50 `infdig` ở Tạo báo giá mẫu; N51 ô NCC trống + lỗi parse.
- SAU khi sửa: đo lại từng màn (DOM + console sạch); màn Danh sách hàng hoá ERP 0 nút xuất, toolbar không lệch; N41 đếm tem Mẫu 1 không có hàng mẫu 2; bố cục chi tiết hàng hoá 1440/390.

## Phạm vi xin "làm"
| | |
|---|---|
| Repo / nhánh | ERP worktree `wt-erp-2d1`, nhánh `feat/cc-loi-cu-erp` từ `feat/2d1-erp-khong-loi`; merge LOCAL, push khi user báo. Tài liệu: hrm-claude-config (CLAUDE.md ERP) |
| File | barcode.blade.php (PNK), ProductsController, routes/web.php, app/Product.php, Model/ProductInfo/BaseProduct.php, products/list.blade.php (+ products/pdf.blade.php nếu chỉ phục vụ PDF), tests/Feature/ExampleTest + test mới, calculateDeliveryCost.blade.php, QuotationTemplate.blade.php, products/formShow.blade.php |
| DB | `hrm_erp_giacty`: chỉ đọc + role tạm Playwright (gỡ khi xong). Không migration/seeder/quyền mới |

### Kết quả thực hiện — 2026-10-13
- ERP `feat/cc-loi-cu-erp` `81eef9f9c2` ⇒ merge LOCAL `72b1ba9001` vào `feat/2d1-erp-khong-loi` (CHƯA push). Tài liệu: `hrm-claude-config/erp/CLAUDE.md` Laravel 6 (chưa commit hrm-claude-config).
- Thêm ngoài plan: menu `topmenubar` mục "Hàng chưa có công khoán" (gọi route vừa gỡ — không gỡ là vỡ MỌI trang); `product_templates/list.blade.php` (màn đã chặn "chuyển HRM") gỡ nút/modal xuất + 4 dòng comment vẫn gọi `route()`; N41 tách `ProductsController::inBarcodeSheet` (test được trên sqlite); `ProductMovedToHrmRoutesTest` chuyển 5 route xuất từ danh sách trắng sang danh sách "phải gỡ". Giữ `product.downloadFile` (header, dùng chung file tồn kho), class ProductReportExport/Norm, ProductMailJob, view `products/pdf` (controller khác còn dùng).
- Playwright MCP ERP 8090 (`e2e_assign`, role tạm `CC_UAT_TMP` 118812 — đã gỡ, roles 130 · rhp 20.958 · ehr 1.718 về mốc; server tắt đúng PID 93787/93795):
  - TRƯỚC: N46 PNK-10222 bảng tem 0 dòng + `ReferenceError: WarehouseImportArrangeDelivery is not defined`; N49 `Cannot read properties of undefined (reading 'cost')`, giá cũ 123 còn nguyên; N50 `$rootScope:infdig` ở Tạo báo giá mẫu; N51 `$parse:syntax`, ô NCC rỗng (hàng 10654 có 2 NCC).
  - SAU: N46 bảng tem 4 dòng, console sạch; N49 toast "Không tìm thấy xe và trọng tải phù hợp trong bảng giá hiệu lực", cost/km = null, không lỗi; N50 console sạch; N51 "CTY DTH VIỆT NAM, CỦA HÀNG LẺ", bố cục 2 cột 1050/330 không tràn (1440); Danh sách hàng hoá: toolbar còn "Cập nhật giá (HRM) · Thùng rác · Tùy chỉnh cột", 0 nút xuất, 0 modal xuất, menu không còn "Hàng chưa có công khoán", `/admin/products/exportExcel` 404, console sạch (chỉ 404 ảnh có sẵn).
  - N41 KHÔNG đo trên trình duyệt (cần phiếu nhập có cả hàng mẫu 1 + mẫu 2) — chốt bằng PHPUnit `inBarcodeSheet` (chuỗi / số).
- PHPUnit ERP **93/93** (trước: 1 đỏ sẵn ExampleTest). Không log lỗi Laravel ERP hôm nay.
- Còn lại ngoài phạm vi: `tmp_products/exportExcel|exportCSV|exportPDF` (hàng tạm ERP) vẫn còn — chưa hỏi; ghi N89.

### Checkpoint — 2026-10-13 (C-c xong)
Vừa hoàn thành: E1–E9 + D1 + kiểm (PHPUnit 93/93, Playwright trước/sau) — merge LOCAL ERP.
Đang làm dở: không. Server 8090 đã tắt, role tạm đã gỡ.
Bước tiếp theo: (ĐÃ PUSH ERP `ad57aec450`; hrm-claude-config commit `c1bd5c8` chờ push/PR) · rồi C-e (N1) · C-f · A7.
Blocked: —

### N89 + push — 2026-10-13 (user: "Ok cả 2 yêu cầu")
- N89: gỡ 3 route `tmpProduct.exportExcel|exportCSV|exportPDF` + 3 nút màn Quản lý hàng tạm + 3 action TmpProductsController (+ import PDF/FastExcel thừa); test route giữ / vùng trắng cập nhật + ca mới. ERP `feat/cc-n89-tmp-export` ⇒ merge `ad57aec450`. PHPUnit ERP 94/94. Playwright 8090: toolbar chỉ còn "Tùy chỉnh cột", 0 nút xuất, `/admin/tmp_products/exportExcel` 404, console sạch; server tắt đúng PID.
- **ĐÃ PUSH** ERP `feat/2d1-erp-khong-loi` `42bbe92ae2..ad57aec450` (C-c + N89).
- hrm-claude-config: commit `c1bd5c8` CHỈ `erp/CLAUDE.md` (N39) — CHƯA push (repo tài sản chung, quy tắc "sửa qua PR"; các file `.plans` khác đang dở của nhiều đợt không gom).
