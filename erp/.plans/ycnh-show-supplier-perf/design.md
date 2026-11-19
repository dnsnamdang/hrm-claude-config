# Design — Tối ưu màn show YCNH tránh treo trình duyệt

Feature: `ycnh-show-supplier-perf` · 2026-10-29

## Vấn đề

Màn `product_import_requests/{id}/show` treo do nhúng toàn bộ danh mục NCC (~10.757) và
render thành hàng chục nghìn `<option>` trong 5 select (AngularJS 1.3.9 compile cả body).

## Quyết định

- Chỉ sửa **màn show** (chỉ-đọc). Giữ nguyên class JS dùng chung và màn create/edit.
- Nạp đúng tập NCC phiếu dùng: NCC chính + NCC các dòng chi phí (`costs[].supplier_id`,
  gồm foreign type=1, inland type=2). Dữ liệu `costs` đã có sẵn trong `getDataForShow`.

## Thay đổi

1. `app/Http/Controllers/Warehouse/ProductImportRequestsController.php` — `show()`:
   gom supplier_id dùng thật → `Supplier::whereIn('id', $ids)` thay vì `->get()` toàn bộ.
2. `resources/views/warehouse/product_import_requests/show.blade.php`:
   `$scope.form.suppliers = @json($suppliers)` ngay sau khi tạo `$scope.form`
   (các `<option ng-repeat="... in form.suppliers">` sẽ dùng list nhỏ).

## Không làm (ngoài scope)

- Không tối ưu blob customers (~44.948) — không render option, không gây treo.
- Không chuyển create/edit sang select2-ajax (task riêng, chờ user chốt).
