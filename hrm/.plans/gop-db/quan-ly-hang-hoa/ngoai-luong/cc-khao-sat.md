# Khảo sát đợt C-c — lỗi cũ ERP (13/10/2026, chỉ đọc)

> Mục: N39 · N41 + N46 · N43 · N44 · N45 · N49 · N50 · N51 (N47/N48 ❌ bỏ qua — user 13/10).
> ERP worktree `wt-erp-2d1` @ `42bbe92ae2` (nhánh chung `feat/2d1-erp-khong-loi`, khớp origin). DB `hrm_erp_giacty`.

| Mục | Hiện trạng (đã đọc code) | Hướng sửa | Cỡ |
|---|---|---|---|
| N39 | `ERP/CLAUDE.md` (symlink `hrm-claude-config/erp/CLAUDE.md`) ghi "Laravel 8"; `composer.json` `^6.2`, vendor cài **6.20.45** | Sửa 1 dòng bảng Tech Stack: "Laravel 6 (`^6.2`, đang cài 6.20.45)" — tài liệu, đẩy qua hrm-claude-config | XS |
| N46 | `warehouse_imports/barcode.blade.php:169-171` include `WarehouseImportLotDetail` + `WarehouseImportLot` + `WarehouseImport` nhưng THIẾU `WarehouseImportArrangeDelivery` — class `WarehouseImport` gọi `new WarehouseImportArrangeDelivery(...)` ngay constructor (`WarehouseImport.blade.php:11`) ⇒ ReferenceError, cả màn in tem trống. 5 view khác cùng nhóm đều include đủ | Thêm `@include('partials.classes.warehouse.WarehouseImportArrangeDelivery')` | XS |
| N41 | `ProductsController::barcode()` nhánh `twoCode == 'false'` (nút "Mẫu 1") vẫn `array_push` mọi hàng (comment 2-D1 giữ hành vi cũ) | Q-N41 ✅: lọc bỏ hàng `barcode_template_type == 2` ở nhánh `false` (so `(int)`) | XS |
| N43 | `App\Model\ProductInfo\BaseProduct::isRequiredSeri()` gọi `Product::query()` — trong namespace `App\Model\ProductInfo` ⇒ class không tồn tại. Không ai gọi (2 chỗ gọi đều là `App\Product::isRequiredSeri`, kế thừa `App\BaseProduct`) | Xoá method chết | XS |
| N44 | (a) `products/exports/product_export.blade.php:60` `$baseUnit->name` khi hàng không có ĐVT cơ bản ⇒ lỗi cả file (dùng ở xuất Excel < 400 dòng, job gửi mail ≥ 400 dòng và `ProductInfoController`); (b) `App\Product::exportExcel()` (PhpSpreadsheet) chết — chỗ gọi duy nhất đã comment (`ProductMailJob:41`); (c) route `products.exportCSV` / `products.exportPDF` (`web.php:580-581`) KHÔNG có nút nào gọi; CSV `->model->name` / `->base_unit->name` nổ khi null; PDF ghim `$host = 'http://localhost:8000'` | (a) `$baseUnit->name ?? ''`; (b) xoá; (c) **chờ chốt C-c-1** | S |
| N45 | `tests/Feature/ExampleTest` `get('/')` ⇒ 302 (middleware `sso.check`) mà assert 200 ⇒ bộ PHPUnit ERP luôn đỏ 1 ca | Tự chốt: đổi thành ca có nghĩa — chưa đăng nhập vào `/` ⇒ chuyển hướng (302), không 500 | XS |
| N49 | `calculateDeliveryCost.blade.php:82` `response.data.cost`: `getCost` trả lỗi bằng `responseErrors()` — **HTTP 200** + `success:false`, không có `data` (`ResponseTrait.php:33`, bỏ qua `$code`) ⇒ nhánh `success` của `$.ajax` chạy ⇒ `reading 'cost'`. Xảy ra khi công ty chưa có bảng giá vận chuyển / không có xe-trọng tải / tuyến phù hợp | FE: `response.success === false` ⇒ báo `response.message` (toastr như các màn ERP), xoá `cost`/`km` cũ; giữ BE (đổi `responseErrors` là sửa hàm dùng chung) | S |
| N50 | `QuotationTemplate.blade.php:46` getter `products` trả `this._products \|\| []` ⇒ khi chưa có hàng, MỖI lần đọc ra MẢNG MỚI ⇒ `ui-sortable ng-model` / watcher thấy đổi mãi ⇒ `$rootScope:infdig` (màn Tạo/Sao chép báo giá mẫu) | Getter tự gán `this._products = []` 1 lần rồi trả cùng tham chiếu; rà getter mảng khác cùng file | S |
| N51 | `products/formShow.blade.php:923` `ng-value="(product.suppliers \|\| []).map(function (s) {...}).join(', ')"` — Angular 1.3.9 không cho `function` trong biểu thức ⇒ lỗi parse, ô Nhà cung cấp trống | Tính sẵn chuỗi ở controller (`$scope.supplierNames`) hoặc hàm scope; đo lại bố cục chi tiết hàng hoá (sau C-a2 bỏ ô Giá vốn/Giá mua) | S |

## Chốt
| # | Câu | Đáp án |
|---|---|---|
| C-c-1 | 2 route `products.exportCSV` / `products.exportPDF` không có nút gọi, CSV nổ khi thiếu Model/ĐVT, PDF ghim localhost | ✅ 13/10 user: "Bên ERP không dùng các chức năng này nữa, sẽ làm mới bên HRM sau" ⇒ **gỡ** 2 route + 2 action + `Product::exportExcel` chết (không vá). Dòng `$baseUnit->name` của file Excel vẫn vá (nút Xuất Excel + job mail + ProductInfoController còn gọi) |

## Tự chốt (không phải nghiệp vụ)
- N45: giữ 1 ca smoke có nghĩa thay vì xoá file.
- N49: không sửa `ResponseTrait::responseErrors` (dùng chung, trả 200 ở mọi nơi) — chỉ xử ở chỗ gọi.

### Bổ sung chốt 13/10 (sau C-c-1)
| # | Câu | Đáp án |
|---|---|---|
| C-c-1b | Xuất Excel hàng hoá ERP | ✅ user: "Xuất excel cũng bỏ luôn, tôi sẽ làm bên HRM sau" |
| C-c-2 | Phạm vi gỡ ở màn Danh sách hàng hoá ERP | ✅ **gỡ hết**: nút "Xuất Excel" + popup chọn cột (`exportProduct`), nút "Hàng chưa có công khoán" (`exportExcelNorm`), route ẩn `exportExcel` (+ job mail ≥ 400 dòng), `exportCSV`, `exportPDF` + action trong ProductsController + `Product::exportExcel` chết. Class `ProductReportExport` / `ProductReportExportNorm` / `ProductMailJob` GIỮ (controller cũ ProductInfo / ProductTemplates / ProductApproves / Product2 còn tham chiếu, không route) ⇒ KHÔNG vá dòng `$baseUnit->name` nữa |

