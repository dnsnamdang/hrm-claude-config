# Nhóm máy lấy từ danh mục Loại SP (10/11/2026)

User chốt: tab Nhóm máy (form hàng hoá) + cột Nhóm máy (import) lấy từ `product_types` thay `groups`.
Dữ liệu cũ: ghép theo TÊN nhóm hàng hoá cũ = tên Loại SP → chuyển; không khớp → XOÁ (PTKD chọn lại).
Sửa cả ERP (popup tìm phụ tùng theo máy + lọc "Dùng cho nhóm máy") — xem ERP/.plans/nhom-may-theo-loai-sp.

Lưu: `productables.productable_type = Modules\MasterData\Entities\ProductClassification\ProductType`
(hằng `Productable::TYPE_PRODUCT_TYPE`), `productable_id = product_types.id`.
Lọc phụ tùng theo máy: so `products.product_type_id` của máy.

Worktree: HRM/hrm-api-nmlsp, HRM/hrm-client-nmlsp (nhánh fix/nhom-may-loai-sp từ origin/develop).

## Tasks
- [x] T1 Productable: hằng TYPE_PRODUCT_TYPE
- [x] T2 Options form + nhân bản: machine_groups lấy product_types
- [x] T3 Request exists:product_types; WriteService ghi kiểu mới
- [x] T4 Form/Detail resource, History, Copy service đọc kiểu mới + bảng product_types
- [x] T5 Import: catalog machine_group → product_types
- [x] T6 Picker báo giá DV: lọc theo product_type_id của máy
- [x] T7 Migration: backup dòng Group → bảng productables_group_backup_20261110; ghép theo tên → chèn kiểu mới; xoá dòng Group
- [x] T8 Test feature 12 file MasterData Product đạt (Lifecycle 2 lỗi FK do DB local thiếu khoá ngoại — có sẵn); migration ĐÃ chạy local 10/11 (136 chuyển, 3.756 xoá, backup 3.892), CHƯA bấm trình duyệt

## Phản hồi Redmine #12012 (10/11/2026) — lỗi lưới phải kèm mã hàng
QA: "Khi thông báo, nếu lỗi đó đi kèm mã hãy bổ sung thêm mã hàng hóa bị lỗi" (ảnh: CT lắp ráp - ĐVT, Phụ kiện - ĐVT không nói mã nào).
- [x] R1 ProductImportValidator::kitGrid: lỗi phát sinh khi xét phần tử thứ i mà chưa chứa mã → tiền tố `Mã "CODE": `
- [x] R2 Test: lỗi ĐVT phụ kiện/CT lắp ráp có mã; lỗi đã có mã không bị lặp tiền tố
