# Design — Thêm cột "Ghi chú" vào kết xuất Excel danh sách hàng hóa

**Người phụ trách:** @khoipv

## Mục tiêu

Người dùng cần xem được nội dung ô "Ghi chú" (tab Thông tin bổ sung của hàng hóa) ngay trong file Excel
kết xuất từ màn danh sách `category/product`.

## Scope

- Chỉ thêm 1 cột chọn xuất mới, không đổi bảng hiển thị trên UI, không đổi DB.
- Field: `products.additional_info`.

## Các quyết định

| Vấn đề | Quyết định |
|---|---|
| Sinh file ở đâu | Giữ nguyên cơ chế hiện tại — FE sinh bằng ExcelJS từ API list |
| Id trường xuất | `30` (nối tiếp dải id hiện có, tránh đánh lại số các trường cũ) |
| Vị trí cột | Sau "Ghi chú đặc biệt", trước "Người tạo" — 2 loại ghi chú nằm cạnh nhau |
| Endpoint export BE cũ | Sửa đồng bộ (ProductExport + blade) để 2 nguồn không lệch cột |

## File thay đổi

- `hrm-thanhan-client/pages/category/product/index.vue` — `fieldsExport`, `checkAllField()`
- `hrm-thanhan-api/app/ExcelExport/ProductExport.php` — `$arrayField`
- `hrm-thanhan-api/resources/views/exports/product_report.blade.php` — header + cell

## Downstream impact

Không có. Cột chỉ xuất hiện khi người dùng chủ động chọn trong popup "Xuất danh sách".
