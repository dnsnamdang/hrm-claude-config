# HDSD màn "Yêu cầu nhập hàng" (ERP TanPhatDev)

Tài liệu Hướng dẫn sử dụng cho người dùng cuối, màn **Yêu cầu nhập hàng**
(Phiếu Yêu cầu nhập hàng — `admin/warehouse/product_import_requests`).
Làm tương tự HDSD "Yêu cầu xuất hàng" (xem `ERP/.plans/hdsd-yeu-cau-xuat-hang/`).

- **Output:** `ERP/HDSD_luongchinh/HDSD_YeuCauNhapHang.docx`
- **Generator:** `gen_hdsd_ycnh_erp.py` (cùng thư mục này).
- **Không chèn ảnh** (user chốt không cần) → dùng box "[Vị trí chèn ảnh] …".

## Nguồn khảo sát (ERP/TanPhatDev)
- Controller: `app/Http/Controllers/Warehouse/ProductImportRequestsController.php`
- Model: `app/Model/Warehouse/ProductImportRequest.php` (+ `ImportModel.php`, `ProductImportRequestDetail.php`)
- Views: `resources/views/warehouse/product_import_requests/` (index, all, forManager, forDepartmentManager, forAccounting, create, edit, form, formJs, show, history)
- Class Angular: `resources/views/partials/classes/warehouse/ProductImportRequest.blade.php`
- Routes: `routes/web.php` (prefix admin/warehouse/product_import_requests)
- Menu: `resources/views/layouts/topmenubar.blade.php`
- Quyền: `database/seeds/PermissionsTableSeeder.php`; cấu hình duyệt `DueConfigsTab2Seeder.php`

## Cách dựng lại
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-yeu-cau-nhap-hang/gen_hdsd_ycnh_erp.py
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

## Điểm khác biệt so với màn Yêu cầu xuất hàng
- Màn nhập **KHÔNG có chức năng xóa hẳn** — chỉ có **Hủy** (chuyển trạng thái Đã hủy).
- Duyệt theo **GIÁ hàng trả lại** (Ban kiểm soát → BGĐ) + **TP duyệt** (bán/bán khi mượn trả lại),
  KHÔNG theo hạn mức công nợ như màn xuất.
- 3 nhánh duyệt: (1) thường → Kế toán kho lập đề nghị nhập kho / phiếu nhập hàng;
  (2) bán trả lại / bán (khi mượn) trả lại thường → Chờ TP duyệt;
  (3) hàng trả lại có quyết toán → Chờ ban kiểm soát duyệt giá → BGĐ.
- Bước tiếp: Kế toán kho "Tạo đề nghị nhập kho" (nhập thường) hoặc "Tạo phiếu nhập hàng" (nhập thẳng).

## Cấu trúc tài liệu
Bìa → Mục lục → Danh mục hình → TỔNG QUAN (thuật ngữ, lịch sử, giới thiệu +
đường dẫn menu, quyền & phạm vi) → PHẦN 1 Truy cập & bố cục → PHẦN 2 Danh sách
(bảng quyền đầy đủ + tiểu mục theo quyền, lọc, cột, nút hành động, trạng thái) →
PHẦN 3 Tạo (chọn loại, trường theo loại, bảng hàng + tab chi phí, nút lưu, validate) →
PHẦN 4 Xem & Duyệt (3 nhánh: Kế toán kho / TP / Ban kiểm soát → BGĐ) →
PHẦN 5 Hủy phiếu (không có xóa) → PHẦN 6 In & Excel & Lịch sử →
PHẦN 7 Màn duyệt/kế toán → PHẦN 8 FAQ.
