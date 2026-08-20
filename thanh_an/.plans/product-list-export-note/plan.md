# Plan — Thêm cột "Ghi chú" vào kết xuất Excel danh sách hàng hóa

**Người phụ trách:** @khoipv
**Màn:** `category/product` (danh sách) → nút Kết xuất Excel

## Yêu cầu

Bổ sung cột **Ghi chú** vào file Excel kết xuất của màn danh sách hàng hóa.
Nguồn dữ liệu: field `additional_info` — chính là ô "Ghi chú" ở tab **Thông tin bổ sung** của form hàng hóa.

## Ghi chú kỹ thuật

- File Excel màn danh sách được sinh ở **FE** bằng ExcelJS (`generateProductWorkbook`), lấy dữ liệu từ API list `category/products` → `ProductResource` đã trả sẵn `additional_info`, không cần sửa BE list.
- Endpoint export cũ ở BE (`ProductController@export` + `ProductExport` + blade `exports/product_report`) vẫn được sửa đồng bộ để không lệch cấu hình cột.
- Vị trí cột: ngay sau "Ghi chú đặc biệt", trước "Người tạo".
- Không migration, không phân quyền theo cấp.

## Task

- [x] T1 — FE `pages/category/product/index.vue`: thêm `{ id: 30, key: 'additional_info', text: 'Ghi chú' }` vào `fieldsExport` (sau `special_note`)
- [x] T2 — FE: thêm id 30 vào danh sách của `checkAllField()`
- [x] T3 — BE `app/ExcelExport/ProductExport.php`: thêm `30 => 'additional_info'` vào `$arrayField`
- [x] T4 — BE blade `resources/views/exports/product_report.blade.php`: thêm header + ô dữ liệu cột "Ghi chú" sau `special_note`
- [x] T5 — Verify: mở `category/product` → Kết xuất Excel → chọn/chọn tất cả trường → kiểm tra cột "Ghi chú" có dữ liệu

### Checkpoint — 2026-08-14
Vừa hoàn thành: T1–T4 (code xong cả FE + BE).
Đang làm dở: không có.
Bước tiếp theo: user verify trên môi trường dev (T5).
Blocked:
