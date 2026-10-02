# Phiếu xuất hàng — Loại xuất điều chuyển chi nhánh: bổ sung cột %VAT

Redmine #11319 (Ưu tiên Cao) — @junfoke. Repo `TanPhatDev`, nhánh `task_11319` (checkout từ `master`).

## Mục tiêu

Màn **Phiếu xuất hàng** (`product_exports`), với **loại xuất "Xuất điều chuyển kho chi nhánh"** (`type == 7`,
`ExportModel::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH`): bổ sung **cột "% VAT"** hiển thị **% VAT của hàng hóa**.

## Quyết định (chốt với user 2026-09-05)

- **Nguồn dữ liệu**: `products.vat_percent` — **% VAT gốc trong danh mục hàng hóa** (Product master), decimal(5,2).
  Chỉ **hiển thị**, không cho sửa, không nhập tay. Điều chuyển nội bộ chi nhánh không có hợp đồng bán nên
  không lấy VAT theo hợp đồng; lấy VAT mặc định của sản phẩm. Áp dụng được cho cả phiếu cũ lẫn mới mà không
  cần nhập lại (khác `product_export_details.vat_percent` — với type 7 đang NULL).
- **Phạm vi màn**: (1) Chi tiết (show), (2) Tạo/Sửa (form), (3) Bản in.

## Hiện trạng code

- `type == 7` = "Xuất điều chuyển kho chi nhánh" (`ExportModel.php`, `constant.js` EXPORT_TYPES id 7).
- Cột "% VAT" hiện chỉ hiện khi `form.type == 4 || form.is_sale` (show/form). `type 7` không thuộc nhóm này.
- `is_sale` = [1,11,13,14,16,17]; `showAllocatedPrice` = [1,4,11,13,14,16,17] (JS `ProductExport.blade.php`).
- Blade Angular đọc được `product.product.vat_percent`: quan hệ `ProductExportDetail::product()` → `App\Product`
  (có cột `vat_percent`, không `$hidden`). Đã eager load ở `getDataForShow`/`getDataForEdit` (`products.with('product')`);
  form create nạp qua AJAX cũng kèm `.product` (đang dùng `product.product.avatar`, `product.units`).

## Điểm cần lưu ý

- **In hạch toán** (`printAccounting` → `getAccountingTableAttribute`) là bảng bút toán Nợ/Có, KHÔNG phải bảng
  hàng hóa → không có chỗ cho cột %VAT theo hàng. Chỉ thêm cột vào **In phiếu** (`print` → `getProductTableAttribute`).
- Các dòng tổng (`colspan="8"`) chỉ render cho is_sale/type3/type4/type17 — type 7 không có → thêm cột không lệch tổng.
- Sub-row kho kế toán không bị ảnh hưởng vì cột %VAT dùng `rowspan="<% product.rowSpan %>"`.

## Files thay đổi

- `resources/views/warehouse/product_exports/show.blade.php` — header + body cột %VAT cho type 7.
- `resources/views/warehouse/product_exports/form.blade.php` — header + body cột %VAT cho type 7.
- `app/Model/Warehouse/ProductExport.php` — `getProductTableAttribute()` thêm cột %VAT (chỉ khi type 7) cho bản in.
