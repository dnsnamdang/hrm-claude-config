# Plan — Thêm nút xem lịch sử giữ hàng cho phiếu Hủy & Gia hạn hàng giữ

## Bối cảnh
Task "Phiếu điều chuyển, gia hạn, hủy hàng giữ: Thêm icon xem lịch sử giữ hàng" mới chỉ làm
cho phiếu **Điều chuyển** (`prepick_transfer2`). Phiếu **Hủy** (`prepick_cancel_requests`) và
**Gia hạn** (`prepick_extend_requests`) chưa có. User không thấy lịch sử ở:
- `admin/warehouse/prepick_cancel_requests/3012/show`
- `admin/warehouse/prepick_extend_requests/1246/show`

## Quyết định
1. Phạm vi: **toàn bộ màn** của cả 2 phiếu — create, edit, show.
2. UI: **1 nút riêng** trên từng dòng hàng (icon `fa-history`), không bọc vào số lượng.

## Hạ tầng sẵn có
- API: route `warehouseInfo.getHistoryPrepickDetails` (`routes/web.php:923`) →
  `WarehouseInfosController@getHistoryPrepickDetails`. Tham số: `product_id`, `company_id`, `employee_id`, `customer_id`.
- Pattern tham chiếu: `warehouse/prepick_transfer2/show.blade.php` (icon + JS `getHistoryPrepick` + modal `#history-prepick`).
- Data:
  - Hủy: `product.product_id` + customer cấp phiếu (`form.customer_id`).
  - Gia hạn: `product.product_id` + `product.detail.customer_id`.

## Tasks

### Chuẩn bị
- [x] Tạo partial modal dùng chung `resources/views/partials/historyPrepickModal.blade.php`

### Phiếu Hủy (prepick_cancel_requests)
- [x] `formJs.blade.php`: thêm `$scope.getHistoryPrepick` + state + `trustAsHtml` (dùng chung create/edit/show)
- [x] `form.blade.php`: thêm cột "Lịch sử" + nút từng dòng + include modal partial + colspan empty-row 11→12
- [x] `show.blade.php`: thêm cột + nút từng dòng + include modal partial
- [x] `create.blade.php`, `edit.blade.php`, `show.blade.php`: inject `$sce` vào controller

### Phiếu Gia hạn (prepick_extend_requests)
- [x] `formJs.blade.php`: thêm `$scope.getHistoryPrepick` + state + `trustAsHtml` (dùng chung create/edit)
- [x] `form.blade.php`: thêm cột + nút từng dòng + include modal + total row +1 td + empty colspan 10→13
- [x] `show.blade.php`: thêm cột + nút từng dòng + include modal + **getHistoryPrepick inline** (show KHÔNG include formJs) + total row +1 td
- [x] `create.blade.php`, `edit.blade.php`, `show.blade.php`: inject `$sce` vào controller

### Lưu ý kỹ thuật
- API `getHistoryPrepickDetails` lọc `PrepickDetail` theo product_id + company_id + customer_id + **employee_id (người giữ = người tạo phiếu)** → truyền `employee_id = form.created_by || DEFAULT_USER.id` (không dùng Auth::id như transfer2, vì approver có thể xem).
- Customer: Hủy = cấp phiếu (`form.customer_id`); Gia hạn = cấp dòng (`product.detail.customer_id`).

### Kiểm tra
- [x] Soát cú pháp Angular/Blade bằng mắt + grep nhất quán (6 controller $sce, 4 nút, 4 modal, 4 header, 3 JS def)
- [ ] Test thủ công 6 màn (create/edit/show × 2 phiếu): nút hiện, click ra modal, có data
  - Test URL user báo: `prepick_cancel_requests/3012/show`, `prepick_extend_requests/1246/show`

### Checkpoint — 2026-06-17
Vừa hoàn thành: code toàn bộ 11 file (1 partial mới + 10 blade sửa) cho cả 2 phiếu Hủy + Gia hạn, đủ create/edit/show.
Đang làm dở: (không)
Bước tiếp theo: user test thủ công 6 màn, đặc biệt 2 URL đã báo.
Blocked: cần kiểm tra company_id khi approver khác công ty xem (hiện dùng company của người xem — có thể rỗng history nếu lệch công ty).
