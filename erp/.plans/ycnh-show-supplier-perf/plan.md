# Plan — Sửa màn show YCNH (product_import_requests) treo trình duyệt

Feature: `ycnh-show-supplier-perf`
Ngày: 2026-10-29

## Bối cảnh

URL `admin/warehouse/product_import_requests/{id}/show` (vd phiếu 13060) vào rất chậm
rồi "không vào được" (trình duyệt treo).

## Nguyên nhân gốc (đã xác định)

- Class JS dùng chung `partials/classes/warehouse/ProductImportRequest.blade.php` dòng 15:
  `this.suppliers = @json(Supplier::getForSelect())` → nhúng **~10.757 NCC** vào `form.suppliers`.
- Trong `show.blade.php` có **5 khối** `<option ng-repeat="... in form.suppliers">`
  (1 select NCC chính + 4 select trong các dòng chi phí: inland_costs ×2, foreign_costs,
  foreign_costs_not_tax). AngularJS 1.3.9 compile toàn bộ `<body>` → số DOM `<option>` =
  (số select) × 10.757 (vài chục nghìn node) + watcher `ng-repeat`/`ng-selected` → **treo**.
- Backend `getDataForShow(13060)` chạy tốt (~117 query), KHÔNG phải nguyên nhân.
- Customers (~44.948) cũng bị nhúng JSON (class dòng 17) nhưng KHÔNG render thành `<option>`
  trong show → không gây treo (để nguyên, ngoài scope).

## Hướng sửa (Cách A — user đã duyệt)

Màn show chỉ-đọc: mọi select NCC đều `disabled`, chỉ cần hiển thị đúng NCC đã chọn.
→ Chỉ nạp những NCC mà phiếu thực sự dùng (NCC chính + NCC ở các dòng chi phí),
thay vì toàn bộ danh mục.

## Tasks

- [x] T1. `ProductImportRequestsController@show`: gom `supplier_id` được dùng
  (NCC chính `$data['supplier_id']` + `$data['costs'][].supplier_id`), chỉ
  `whereIn` nạp các NCC đó (select `id, code, fullname, short_name` để khớp option text
  `<% s.code %> - <% s.fullname %>`).
- [x] T2. `show.blade.php`: sau khi khởi tạo `$scope.form`, override
  `$scope.form.suppliers = @json($suppliers)` để 5 khối option dùng list nhỏ
  (thay vì list ~10k của class). Không đụng class dùng chung (create/edit giữ nguyên).
- [x] T3. Verify (read-only prod, phiếu 13060): dùng **8 NCC** (1 chính + 7 unique từ 8
  dòng chi phí) → nạp đúng 8 thay vì **10.759**; mọi supplier_id dùng đều resolve ra tên
  (không thiếu) → select disabled vẫn hiện đúng NCC đã chọn. DOM option giảm từ ~chục nghìn
  xuống vài chục → hết treo.

### Checkpoint — 2026-10-29
Vừa hoàn thành: Fix T1+T2, verify T3 (read-only prod). Commit+push gop_db **3be45d8c67**.
User chốt KHÔNG rà create/edit (giữ nguyên).
Đang làm dở: (không)
Bước tiếp theo: User test trực tiếp sau khi deploy.
Blocked: (không)

## Ghi chú

- KHÔNG sửa class dùng chung `ProductImportRequest.blade.php` → create/edit vẫn nạp đủ
  NCC để chọn (đó là màn nhập liệu, cần list đầy đủ; nếu muốn tối ưu create/edit thì
  chuyển sang `select2-ajax` server-side — task riêng, user chưa chốt).
