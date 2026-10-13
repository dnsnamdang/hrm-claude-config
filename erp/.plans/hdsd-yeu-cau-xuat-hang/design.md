# HDSD màn "Yêu cầu xuất hàng" (ERP TanPhatDev)

Tài liệu Hướng dẫn sử dụng cho người dùng cuối, màn **Yêu cầu xuất hàng**
(Phiếu Yêu cầu xuất hàng — `admin/warehouse/product_export_requests`).

- **Output:** `ERP/HDSD_luongchinh/HDSD_YeuCauXuatHang.docx`
- **Generator:** `gen_hdsd_ycxh_erp.py` (cùng thư mục này).
- **Không chèn ảnh** (user chốt không cần) → dùng box "[Vị trí chèn ảnh] …".

## Nguồn khảo sát (ERP/TanPhatDev)
- Controller: `app/Http/Controllers/Warehouse/ProductExportRequestsController.php`
- Model: `app/Model/Warehouse/ProductExportRequest.php` (+ `ExportModel.php`)
- Views: `resources/views/warehouse/product_export_requests/` (index, all, forManager, forAccounting, create, edit, form, formJs, show)
- Class Angular: `resources/views/partials/classes/warehouse/ProductExportRequest.blade.php`
- Hằng số: `public/js/constant.js` (EXPORT_TYPES, STATUSES, TRANSITION_TYPES)
- Menu: `resources/views/layouts/topmenubar.blade.php`
- Quyền: `database/seeds/PermissionsTableSeeder.php`; cấu hình duyệt `DueConfigsTab2Seeder.php`

## Cách dựng lại
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-yeu-cau-xuat-hang/gen_hdsd_ycxh_erp.py
```
Yêu cầu: python 3.12 (`/usr/local/bin/python3`) có `python-docx` + `lxml`.
Generator import `HdsdBuilder` từ skill HRM
(`HRM/.claude/skills/hdsd-documenter/assets/hdsd_engine.py`) và tự dùng
`HDSD_MAU.docx` làm khung.

## Xử lý mục lục trên macOS (không có PowerShell/Word COM)
KHÔNG gọi `builder.finish()`. Thay bằng `finish_macos()` trong generator:
`doc.save()` → `clear_toc_cache()` (xoá text cache field TOC) →
`_set_update_fields()` (bật updateFields=true) → `_purge_orphan_media()` (chạy cuối).
Word/Word-for-Mac tự dựng lại mục lục + danh mục hình khi mở file.
Chi tiết: memory `hdsd-documenter-macos-toc-workaround`.

## Cấu trúc tài liệu
Bìa → Mục lục → Danh mục hình → TỔNG QUAN (thuật ngữ, lịch sử, giới thiệu +
đường dẫn menu, quyền & phạm vi) → PHẦN 1 Truy cập & bố cục → PHẦN 2 Danh sách
(bảng quyền đầy đủ 9 quyền + tiểu mục theo quyền, lọc, cột, nút hành động, trạng
thái) → PHẦN 3 Tạo (chọn loại, trường theo loại, bảng hàng, nút lưu, validate,
cảnh báo quá hạn) → PHẦN 4 Xem & Duyệt (TP→BGĐ, từ chối, nút bước tiếp) →
PHẦN 5 Hủy & Xóa → PHẦN 6 In & Excel → PHẦN 7 Màn duyệt/kế toán → PHẦN 8 FAQ.
