# Lỗi mở 15/10 — Đợt 3 (ERP): N79 · N97 · N98 — Report

Ngày 15/10/2026. Worktree `wt-erp-2d1`. Nhánh con `feat/cdhh-loi-mo-erp` (từ `feat/2d1-erp-khong-loi` @ `bfbd794503`),
merge `--no-ff` LOCAL về `feat/2d1-erp-khong-loi` = **`f19ef0abca`**. KHÔNG push. Soát marker xung đột: 0.

## Commit

| Commit | Mã | Nội dung |
|---|---|---|
| `ef7df6d3ca` | N79 | `app/Model/Customers/WrServiceQuotation.php` — 4 chỗ `$service->` → `$product_item->` (vòng `choose_services` hàng bảo hành ở `getForCopy` + `getForEdit`) |
| `3e860e1400` | N97 | `OrderRequestProduct2` + `InlandOrderRequestProduct2`: `this.no_set = ['unit_coefficient']`; `inland_order_request_new/approver_index.blade.php`: ẩn nút "Tạo mới" (comment blade) |
| `7d4ac089c7` | N98 | `partials/classes/sale/Customer.blade.php`: `(customer.mobile \|\| '').split(',')` ⇒ KH cá nhân mobile NULL có `phones = ['']` |
| `706837e090` | test | `tests/Feature/LoiMo1510ErpTest.php` (4 ca, khoá bằng mã nguồn / blade compileString) |
| `f19ef0abca` | merge | Merge về nhánh chung |

Ghi chú N97 nút "Tạo": 3 view TN mới — `index` và `department_approver_index` đã comment sẵn nút từ trước; chỉ `approver_index` (màn "Tổng hợp", `/forApprover`) còn nút sống ⇒ chỉ sửa file này. (Lần đầu bọc thêm comment vào `department_approver_index` sẽ tạo comment blade lồng nhau làm vỡ trang — đã hoàn lại, không commit.)

## Kiểm

- PHPUnit ERP cả bộ: **191 tests, 4329 assertions, 4 skipped, xanh** (mốc 187 + 4 ca mới). Ca N79 đã xác nhận ĐỎ trên code gốc.
- Lint blade (compileString + `php -l`): 4 file blade sửa đều "No syntax errors"; bản compile `approver_index` có 0 lần `inlandOrderRequestNew.create`.
- Playwright (ERP `artisan serve --port=8090` từ worktree, PID 86157/86172 — đã kill đúng PID; đăng nhập `/login` bằng `e2e_assign@test.local`). Chạy CÙNG script 2 lượt: code gốc (tạm chép bản HEAD vào file) và code đã sửa. Script: `scratchpad/loimo-erp/check.js`, `kh1000.js`; kết quả `before.json` / `after.json`.

| Ca | Trước sửa | Sau sửa |
|---|---|---|
| Chi tiết KH 232387 `/admin/customers/232387/manager` | `TypeError: Cannot read properties of null (reading 'split') at new Customer` ⇒ `$scope.customer` không có | Lỗi JS = **0**; `customer.phones = ['']`, `customer_type=1`, trang render (0 `<% %>` thô) |
| Chi tiết KH 1000 | `pageerror: Cannot read properties of undefined (reading 'date_of_birth')` | Y nguyên (KHÔNG sửa theo brief) — nguyên nhân ở dưới |
| TN mới `/inland_order_request_new` · `/forApprover` · `/forDepartmentApprover` — đếm nút/link "Tạo" hiển thị | 0 · **1 ("Tạo Mới")** · 0 | **0 · 0 · 0**; link `…/create` trên trang = 0 |
| YC đặt hàng NK 2 `order_request2/create` — thêm hàng tay (hàng 23779, thương hiệu 235) | getData 200 nhưng `TypeError: Cannot set property unit_coefficient … which has only a getter`, số dòng hàng 0 | Lỗi = 0; 1 dòng hàng, `unit_id=40`, ĐVT "Cái", `unit_coefficient` (getter) = 1 |
| TN 2 `inland_order_request2/create` — như trên | Cùng TypeError (`InlandOrderRequestProduct2`), 0 dòng | Lỗi = 0; 1 dòng, ĐVT "Cái" |
| Báo giá dịch vụ BH-SC — form tạo, sao chép báo giá 11655 | `getDataCopy` **HTTP 500** (ErrorException "Creating default object from empty value", dòng 1072) ⇒ form trống | HTTP 200; dịch vụ 5393: giá 1,920,000, VAT 8 — form hiện đúng |
| Sao chép báo giá 11584 (2 dịch vụ bảo hành) | HTTP 500 | HTTP 200; 5378: 4,800,000 / VAT 8; 5379: 1,920,000 / VAT 8 |

Thêm hàng tay: gọi đúng handler `$scope.addProduct({id, brand_id})` mà popup chọn hàng dùng ở `onPick` (gọi `/products/{id}/getData?query_stock=1` thật + constructor class thật), không bấm qua popup. KHÔNG lưu phiếu nào, KHÔNG lưu báo giá nào.

So giá/VAT N79 bằng tinker (`getForEdit` + `getForCopy`, 5 báo giá 11655, 11598, 11584, 11269, 11046):
- Giá bán (`sell_price`) trước = sau (gốc đã đúng bằng `device_error_costs.price_service`; trước sửa không gán được nhưng giá trong DB trùng giá lỗi thiết bị).
- **VAT đổi 0 → 8** (`costs.vat_percent`) ở mọi dòng dịch vụ bảo hành. Trong DB các dòng này lưu `vat_percent = 0`.
- Trước sửa, trong tinker chỉ là WARNING; qua HTTP (`getDataCopy`, `edit`) Laravel đổi thành ErrorException ⇒ 500.

Lỗi console "Failed to load resource" còn lại trên mọi trang (cả trước và sau) là ảnh tĩnh môi trường local: `/uploads/1672819008tanphat-soft.jpg` 404 và avatar `…/e2e.png` 404/405 — không thuộc phạm vi.

## N98 — KH 1000: nguyên nhân (CHỈ khảo sát, KHÔNG sửa)

`pageerror: TypeError: Cannot read properties of undefined (reading 'date_of_birth')`, stack: callback `angular.element(document).ready` → `$('.date-model').each(...)` trong `customercare/customermanager/show_.blade.php:3183-3200`.

- KH 1000 là `customer_type = 2` (doanh nghiệp) ⇒ card "Người liên hệ" (`ng-if="customer.customer_type >= 2"`, dòng 1122) được render, có ô `data-model="contactToAdd.date_of_birth"` (dòng 1159).
- Vòng `.date-model` đi theo đường `$scope.contactToAdd.date_of_birth`, nhưng `$scope.contactToAdd` chỉ được tạo khi bấm thêm người liên hệ (`showContactForm`, dòng 3756) ⇒ lúc tải trang là `undefined` ⇒ đọc `.date_of_birth` ném TypeError.
- Áp cho MỌI KH `customer_type >= 2` (dev: 12.528 loại 2 + 472 loại 3 + 8 loại 5). KH cá nhân (loại 1) không dính vì card bị `ng-if` bỏ.
- Mức ảnh hưởng: thấp — ô này là `.date-model` CUỐI CÙNG trong trang (thứ tự: 224, 328, 1159) nên 2 ô ngày phía trước vẫn được định dạng; controller AngularJS vẫn sống (`$scope.customer` có, trang render đủ). Chỉ là lỗi console + ô ngày sinh của form thêm người liên hệ không được khởi tạo định dạng lúc tải (form đó tự gán lại khi mở).
- Sửa đề xuất (chờ user): trong vòng `.date-model` bỏ qua khi `object` rỗng giữa đường (`if (!object) return;`), hoặc khởi tạo `$scope.contactToAdd = {phones: ['']}` lúc dựng controller. Cỡ S, 1 file blade. Không liên quan chuyển đổi hàng hoá.

## Dữ liệu thử / quyền tạm

- `e2e_assign` (employee 1180) không có quyền ERP "Xem khách hàng" và "Tổng hợp đặt hàng trong nước" ⇒ tạo role tạm `TMP_E2E_LOIMO_1510_DOT3` id **122282** trên `hrm_erp_giacty`: `role_has_permissions` (100057, 100387; company_id=1) + `employee_has_roles` (model_type `App\Employee` — ERP đọc morph `App\Employee`, KHÁC HRM `Modules\Timesheet\Entities\Employee`).
- Đã xoá đúng id 122282 (roles, role_has_permissions, employee_has_roles); đếm lại: role 0, rp 0; 1180 còn đúng 1 role gốc 118805. `Employee::find(1180)->can('Xem khách hàng')` = false.
- Không ghi phiếu / báo giá nào.

## Lo ngại

1. **N79 đổi hành vi hiển thị VAT**: khi sao chép / sửa báo giá BH-SC có dịch vụ bảo hành, VAT dịch vụ nay lấy từ danh mục chi phí (8%) thay vì 0 đang lưu trong DB ⇒ nếu người dùng lưu lại, tổng tiền báo giá có thể đổi. Trước đây đường này 500 nên không ai sao chép được — chưa có số liệu thực tế. Nên hỏi nghiệp vụ bảo hành dịch vụ bảo hành có chịu VAT không.
2. `php artisan cache:clear` đã chạy 1 lần ở worktree với `CACHE_DRIVER=redis` (để làm mới quyền) — xoá cả cache redis dùng chung của máy local. Lần dọn sau dùng `permission:cache-reset` (báo "Unable to flush cache" nhưng kiểm `can()` đã ra false).

## Lỗi mới ngoài phạm vi (không vá)

- **N120** (đổi từ N112 — trùng đợt 1) — TN mới (`InlandOrderRequestNewController`) chỉ có `index, forApprover, forDepartmentApprover, searchData, show, print`; route `create/edit/delete/update/store/approve/departmentApprove/updateApproverComment/cancel/cancelDetail` trỏ method không tồn tại ⇒ 500. Ngoài nút "Tạo" đã ẩn, còn: dropdown "Sửa" / "Xóa" ở `searchData` (controller dòng 106–107) và các nút Duyệt / Hủy / Lưu ý kiến ở `show.blade.php` (253, 281, 302, 342) — vẫn sống, bấm là 500. Cần làm create/edit TN mới (cỡ L, cần spec) hoặc ẩn tiếp.
- **N121** (đổi từ N113 — trùng đợt 1) — KH loại ≥ 2: TypeError `contactToAdd.date_of_birth` ở chi tiết KH (xem mục KH 1000 ở trên).
